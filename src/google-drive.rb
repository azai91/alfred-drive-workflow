#!/usr/bin/ruby
require 'socket'
require 'net/http'
require 'net/https'
require 'uri'
require 'json'
require 'webrick'
require 'shellwords'
require 'fileutils'
require 'logger'
require 'tempfile'

CLIENT_ID       = '978117856621-tvpnqtr02b8u0bgnh75sqb1loq1f5527.apps.googleusercontent.com'
CLIENT_SECRET   = 'rty2NIATZfWFWSDX-XPs2usX'
REDIRECT_URL    = 'http://127.0.0.1:1337'

BUNDLE_ID       = ENV['alfred_workflow_bundleid'] || 'com.drive.azai91'
CACHE_DIR       = ENV['alfred_workflow_cache']    || "/tmp/#{BUNDLE_ID}"

EJECT_ICON_PATH = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/EjectMediaIcon.icns'

MIME_TYPE_ICONS = {
  'application/vnd.google-apps.document'     => { :path => 'icons/doc.png'   },
  'application/vnd.google-apps.spreadsheet'  => { :path => 'icons/sheet.png' },
  'application/vnd.google-apps.presentation' => { :path => 'icons/slide.png' },
  'application/vnd.google-apps.form'         => { :path => 'icons/form.png'  },
  'application/pdf'                          => { :path => 'icons/dummy.pdf', :type => 'fileicon' },
}

FileUtils.mkdir_p(CACHE_DIR)

$log = Logger.new(STDERR.tty? ? STDERR : "#{CACHE_DIR}/google-drive.log")
$log.formatter = proc do |severity, datetime, progname, msg|
  "[#{datetime.strftime('%Y-%m-%d %H:%M:%S.%3N')}] [#{Process.pid}] %7s #{msg}\n" % "[#{severity}]"
end

class Keychain
  def self.add(password, account, service, comment = nil, label = nil)
    %x{ /usr/bin/security -q add-generic-password -j #{comment.to_s.shellescape} -l #{(label || service).shellescape} -s #{service.shellescape} -a #{account.shellescape} -w #{password.shellescape} -U }
    $log.error("Exit code #$? from /usr/bin/security while adding generic password for #{account}") if $?.exitstatus != 0
    $?.exitstatus == 0
  end

  def self.find(account, service)
    open("|/usr/bin/security 2>&1 find-generic-password -s #{service.shellescape} -a #{account.shellescape} -g") do |io|
      if io.read =~ /^password:\s+(?:0x(\h+)\s+)?"(.*)"$/
        $1 ? $1.scan(/\h\h/).map { |ch| ch.hex }.pack("C*") : $2
      end
    end
  end

  def self.comment(account, service)
    open("|/usr/bin/security 2>&1 -v find-generic-password -s #{service.shellescape} -a #{account.shellescape}") do |io|
      if io.read =~ /^attributes:\n(^\s+.*\n)+/m
        if $1 =~ /^\s+"icmt"<blob>=(?:0x(\h+)\s+)?"(.*)"$/
          $1 ? $1.scan(/\h\h/).map { |ch| ch.hex }.pack('C*') : $2
        end
      end
    end
  end

  def self.delete(account, service)
    %x{ /usr/bin/security 2>&1 -q delete-generic-password -s #{service.shellescape} -a #{account.shellescape} }
    $log.debug("Deleted generic password for #{account}")
    $?.exitstatus == 0
  end
end

class Auth
  def initialize(host, port)
    @server = TCPServer.new(host, port)
  end

  def accept_token
    $log.debug("Starting HTTP server")
    loop do
      socket = @server.accept

      request = ''
      until (str = socket.gets).chomp.empty?
        request << str
      end

      util = WEBrick::HTTPRequest.new(WEBrick::Config::HTTP)
      util.parse(StringIO.new(request))
      $log.debug("Received HTTP request: #{util.request_line.chomp}")

      token = nil
      if util.request_method == 'GET' && util.path == '/' && util.query.has_key?('code')
        token = Auth.get_token({
          'grant_type'   => 'authorization_code',
          'code'         => util.query['code'],
          'redirect_uri' => REDIRECT_URL,
        })
      end

      response = token.nil? ? "Something went wrong.\n" : "Successfully connected to Google Drive!\n"

      socket.print "HTTP/1.1 200 OK\r\n"
      socket.print "Content-Type: text/plain\r\n"
      socket.print "Content-Length: #{response.bytesize}\r\n"
      socket.print "Connection: close\r\n"
      socket.print "\r\n"
      socket.print response
      socket.close

      # Only serve a single request for ‘GET /’
      break if util.request_method == 'GET' && util.path == '/'
    end
    $log.debug("Stopping HTTP server")
  end

  @service_name = "#{BUNDLE_ID}"

  def self.get_token(options)
    token = nil

    token_url = 'https://www.googleapis.com/oauth2/v3/token'
    response = Net::HTTP.post_form(URI.parse(token_url), options.merge({
      'client_id'     => CLIENT_ID,
      'client_secret' => CLIENT_SECRET,
    }))

    if response.code.to_i == 200
      json = JSON.parse(response.body)
      if json.has_key?('refresh_token')
        Keychain.add(json['refresh_token'], 'drive_refresh_token', @service_name)
        $log.info("Refresh token added to keychain")
      end

      if json.has_key?('access_token')
        $log.warn("Access token has no expiration time") unless json.has_key?('expires_in')
        Keychain.add(json['access_token'], 'drive_access_token', @service_name, json.has_key?('expires_in') ? "Expires: #{(Time.now + json['expires_in'].to_i).iso8601}" : nil, @service_name)
        token = json['access_token']
        $log.info("Access token added to keychain, expires in #{json['expires_in']} seconds")
      else
        $log.error("Access token missing from server response: #{json}")
      end
    else
      $log.error("Server returned #{response.code} when requesting token: #{JSON.parse(response.body)['error_description']}")
    end

    token
  end

  def self.token
    if Keychain.comment('drive_access_token', @service_name) =~ /^Expires: (.*)/
      return Keychain.find('drive_access_token', @service_name) if (Time.parse($1) - Time.now) > 10
      $log.info("Access token expired #{((Time.now - Time.parse($1))/60).round(2)} minutes ago")
    end

    if refresh_token = Keychain.find('drive_refresh_token', @service_name)
      token = get_token({
        'grant_type'    => 'refresh_token',
        'refresh_token' => refresh_token,
      })
      return token unless token.nil?
    end

    uri = URI.parse(REDIRECT_URL)
    server = Auth.new(uri.host, uri.port)
    thread = Thread.new { server.accept_token }

    $log.info('Requesting user authentication via browser')
    auth_url = 'https://accounts.google.com/o/oauth2/auth?' + URI.encode_www_form({
      'client_id'       => CLIENT_ID,
      'redirect_uri'    => REDIRECT_URL,
      'scope'           => 'https://www.googleapis.com/auth/drive',
      'response_type'   => 'code',
      'access_type'     => 'offline',
      'approval_prompt' => 'force'
    })
    %x{ open #{auth_url.shellescape} }

    thread.join

    if token = Keychain.find('drive_access_token', @service_name)
      return token
    end

    abort 'No access token'
  end

  def self.revoke
    if token = Keychain.find('drive_refresh_token', @service_name)
      revoke_url = 'https://accounts.google.com/o/oauth2/revoke'
      response = Net::HTTP.post_form(URI.parse(revoke_url), { 'token' => token })
      if response.code.to_i == 200
        Keychain.delete('drive_access_token', @service_name)
        Keychain.delete('drive_refresh_token', @service_name)
        $log.info("Revoked access token")
        return true
      else
        $log.error("Server returned #{response.code} when revoking token: #{JSON.parse(response.body)['error_description']}")
      end
    else
      $log.warn("Refresh token missing while trying to revoke access")
    end
    false
  end
end

class GoogleDrive
  def self.get_items(token)
    uri = URI.parse('https://www.googleapis.com/drive/v2/files')

    query = {
      'q'          => "trashed=false and (mimeType='application/vnd.google-apps.folder' or #{MIME_TYPE_ICONS.keys.map { |type| "mimeType='#{type}'" }.join(' or ')})",
      'fields'     => 'nextPageToken,items(id,title,alternateLink,mimeType,parents(id,isRoot))',
      'maxResults' => 1000,
    }

    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true

    items = []

    loop do
      uri.query = URI.encode_www_form(query)
      request = Net::HTTP::Get.new(uri.request_uri)
      request.add_field('authorization', "Bearer #{token}")
      response = http.request(request)

      if response.code.to_i == 200
        body = JSON.parse(response.body)
        $log.info("Got #{body['items'].size} items from Google Drive")
        items += body['items']

        next if query['pageToken'] = body['nextPageToken']
      else
        $log.error("Server returned #{response.code} when fetching items from Google Drive: #{JSON.parse(response.body)['error_description']}")
      end

      break
    end

    items
  end
end

class Cache
  @cache_file    = "#{CACHE_DIR}/drive-items.json"
  @cache_max_age = 10*60 # 10 minutes

  class << self
    attr_accessor :needs_update
  end

  def self.get_items
    items = {
      'created' => DateTime.now,
      'items'   => GoogleDrive.get_items(Auth.token),
    }

    io = Tempfile.new('items', CACHE_DIR)
    io << JSON.generate(items)
    io.close
    FileUtils.mv(io.path, @cache_file)

    items
  end

  def self.items
    items = open(@cache_file) { |io| JSON.parse(io.read) } rescue nil

    if items.nil?
      items = get_items
    else
      $log.debug("Loaded #{items['items'].size} items from cache (age: #{((Time.now - Time.parse(items['created']))/60).round(2)} minutes)") unless items.nil?
      @needs_update = (Time.now - Time.parse(items['created'])) > @cache_max_age
    end

    items['items']
  end

  def self.delete
    File.unlink(@cache_file) rescue nil
  end
end

# ========
# = Main =
# ========

start = Time.now
$log.debug("#$0 #{ARGV}")

begin
  if ARGV[0] == '--revoke'
    if Auth.revoke
      STDOUT << "Signed out of Google Drive\n"
    else
      STDERR << "Failed to sign out\n"
    end
    Cache.delete
  elsif ARGV[0] == '--create'
    type = ARGV[1]

    name = (ARGV[2] == '--name' ? ARGV[3] : nil).to_s.strip
    name = name.empty? ? 'Untitled' : name

    token = Auth.token
    uri = URI.parse('https://www.googleapis.com/drive/v3/files?fields=webViewLink')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Post.new(uri.request_uri)
    request['authorization'] = "Bearer #{token}"
    request["content-type"]  = 'application/json'
    request.body = JSON.generate({
      :mimeType => type,
      :name     => name,
    })

    response = http.request(request)
    if response.code.to_i == 200
      body = JSON.parse(response.body)
      if body.has_key?('webViewLink')
        %x{ open #{body['webViewLink'].shellescape} }
        Cache.needs_update = true
      else
        $log.error("No webViewLink in response: #{response.body}")
        STDERR << "Link to new document missing from server response\n"
      end
    else
      $log.error("Server returned #{response.code} when creating document with type #{type}: #{JSON.parse(response.body)['error_description']}")
      STDERR << "Failed to create document.\nServer responded with status #{response.code}\n"
    end
  elsif ARGV[0] == '--filter'
    filter, name = ARGV[1].to_s.strip, 'Untitled'
    filter, name = *filter.split(/\s+/, 2) if filter =~ /\s\S/

    res = [
      [ 'Document',     'doc',   '6EA9C89F-E56A-4DD5-AF21-870869D441E6' ],
      [ 'Spreadsheet',  'sheet', 'ACAA585E-C8CE-4D64-AE64-2AD41F6CA9F5' ],
      [ 'Presentation', 'slide', 'EB4B6437-13DB-4E65-9F7D-5BE060E37649' ],
      [ 'Form',         'form',  '3D2966E3-0639-411D-8334-E1926B8626CF' ]
    ].map do |arr|
      {
        :title     => "New #{arr[0]}",
        :subtitle  => "Name: ‘#{name}’",
        :icon      => { :path => "icons/#{arr[1]}.png" },
        :variables => { :action => '--create', :name => name },
        :arg       => "application/vnd.google-apps.#{arr[0].downcase}",
        :uid       => arr[2],
      }
    end

    res << {
      :title     => 'Sign out of Google Drive',
      :icon      => { :path => EJECT_ICON_PATH },
      :variables => { :action => '--revoke' },
      :arg       => 'revoke',
      :uid       => '87B64A2A-F6CE-461C-9A2F-303719D20EFE',
    }

    filter_regex = /#{filter.split(//).map { |ch| Regexp.escape(ch) }.join('.*?')}/i
    res = res.select { |item| item[:title] =~ filter_regex }

    filter = ARGV[1].to_s
    filter_regex = /#{filter.split(//).map { |ch| Regexp.escape(ch) }.join('.*?')}/i

    if items = Cache.items
      parents_by_id = { }
      folders = items.select { |item| item['mimeType'] == 'application/vnd.google-apps.folder' }
      folders.each { |item| parents_by_id[item['id']] = item }

      files = items.reject { |item| item['mimeType'] == 'application/vnd.google-apps.folder' }
      files = files.select { |item| item['title'] =~ filter_regex }
      files = files.sort { |lhs, rhs| lhs['title'] <=> rhs['title'] }

      res += files.map do |item|
        parents = []
        parent = item['parents'].first
        while parent && parent.has_key?('isRoot') && parent['isRoot'] == false
          if parent = parents_by_id[parent['id']]
            parents << parent['title']
            parent = parent['parents'].first
          end
        end

        {
          :uid       => item['id'],
          :title     => item['title'],
          :subtitle  => parents.reverse.join('/'),
          :icon      => MIME_TYPE_ICONS[item['mimeType']],
          :arg       => item['alternateLink'],
          :variables => { :action => '--open' },
        }
      end
    end

    container = { :items => res }
    container[:rerun] = 0.8 if Cache.needs_update
    STDOUT << JSON.generate(container)
  else
    $log.error("Unknown argument")
  end
rescue Exception => e
  $log.fatal("Uncaught exception: #{e}")
end

$log.debug("Execution took #{(Time.now - start).round(3)} seconds")

if Cache.needs_update
  Process.daemon

  begin
    open("#{CACHE_DIR}/lockfile", File::RDWR|File::CREAT) do |io|
      if io.flock(File::LOCK_EX|File::LOCK_NB)
        $log.debug("Start background cache update")
        Cache.get_items
        $log.debug("Finished background cache update")
      else
        $log.debug('Skip background cache update: Another process is already running')
      end
    end
  rescue Exception => e
    $log.fatal("Uncaught exception: #{e}")
  end
end
