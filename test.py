'''
  hello
  command = user_input.split()[0]
  options = user_input[len(command) + 1:]
  if command == '>':
    if options in 'login':
      wf.add_item(title='Drive > login',
          arg=prepend_action_string('login',oauth.get_auth_url()),
          icon=ICON_USER,
          subtitle='Login',
          valid=True)
    if options in 'logout' and wf.stored_data('google_drive_oauth_code'):
      wf.add_item(title='Drive > logout',
        arg='logout',
        icon=ICON_USER,
        valid=True)
    wf.send_feedback()
    return 0
  elif wf.stored_data('google_drive_oauth_code'):
    credentials = wf.stored_data('google_drive_oauth_code')
    results = json.loads(content)['items']
    for result in results:
      type = ""
      try:
        type = result['mimeType'].split('.')[2]
      except:
        type = ""
      if type == 'spreadsheet':
        wf.add_item(title=result['title'],
          arg=result['alternateLink'],
          icon='./assets/sheets.png',
          valid=True)
      elif type == 'document':
        wf.add_item(title=result['title'],
          arg=result['alternateLink'],
          icon='./assets/docs.png',
          valid=True)
    if len(results) == 0:
      wf.add_item(title="No Results Found",
        icon=ICON_WARNING)
      wf.send_feedback()
      return 0
  else:
    wf.add_item(title='Drive > login',
      arg=prepend_action_string('login', oauth.get_auth_url()),
      icon=ICON_USER,
      subtitle=get_auth_url(),
      valid=True)

  '''