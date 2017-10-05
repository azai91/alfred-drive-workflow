# Google Drive Workflow for [Alfred](http://www.alfredapp.com/)

This workflow searches your Google Drive and will open selected files in your browser. The keyword is `d` (example `d alfred`).

With <kbd>↩</kbd> you can open the entry in your default browser.

With <kbd>⌘C</kbd> you can copy the link to your clipboard.

**Please see [troubleshooting](#troubleshooting) if you encounter any problems and star this repo if you find it useful :)**

[Download](https://github.com/azai91/alfred-drive-workflow/releases/latest)

## Requirements

This workflow relies on features introduced in Alfred version 3.4.1.

## Getting Started

The first time you use this workflow, you will be asked (in your default browser) to allow “Alfred Drive Workflow” to view and manage files in your Google Drive.

After successfully connecting the workflow to your Google Drive you can search it from Alfred using `d {query}`.

## Commands

- `d {query}`
Search your Google Drive for files that match the query. You can open the file in your default browser by selecting the file and hitting `enter`

- `d New Document {name}`
Create a new Google Document and open it in your default browser. Name is optional and defaults to `Untitled`.

- `d New Spreadsheet {name}`
Create a Google Spreadsheet and opens it in your default browser. Name is optional and defaults to `Untitled`.

- `d New Presentation {name}`
Create a Google Presentation (slide) and opens it in your default browser. Name is optional and defaults to `Untitled`.

- `d New Form {name}`
Create a Google Form and opens it in your default browser. Name is optional and defaults to `Untitled`.

- `d Update to Google Drive version 1.x`
This action is only available when there is an update. It will download the update and ask Alfred to install it.

- `d Sign out of Google Drive`
Disconnect the workflow from Google Drive and delete access tokens.

## Configuration

You can set [Workflow Environment Variable][1] to control some aspects of this workflow.

### `custom_query`

This will be `and`’ed with the query used for getting files from Google Drive. See [Searching Files](https://developers.google.com/drive/v2/web/search-parameters) for syntax, some examples:

- Exclude all folders and PDF files from search results: `mimeType != 'application/pdf' and mimeType != 'application/vnd.google-apps.folder'`
- Limit search results to items in the folder with ID `0Bx_0bq…F2N`: `'0Bx_0bq…F2N' in parents`

To find the ID of a specific folder, navigate to that folder in your web browser and should be able to see the ID in the URL.

### `open_args`

If you want to open links in a specific browser you can create a [Workflow Environment Variable][1] named `open_args` with a value of:

- Safari:  `-b com.apple.Safari`
- Firefix: `-b org.mozilla.firefox`
- Chrome:  `-b com.google.Chrome`

[1]: https://www.alfredapp.com/help/workflows/advanced/variables/

## Troubleshooting

If you see wrong behavior you are welcome to open an issue but please include the log file!

The log file can be found as `~/Library/Caches/com.runningwithcrayons.Alfred-3/Workflow Data/com.drive.azai91/google-drive.log`.

When pasting it into an issue, be sure to either indent each line with a tab character / four spaces or surround it with three back-ticks like this:

	```
	# Logfile created on 2017-10-05 08:51:37 +0200 by logger.rb/41954
	[2017-10-05 08:51:37.001] [42968] [DEBUG] ./google-drive.rb ["--filter", "f"]
	[2017-10-05 08:51:37.053] [42968]  [INFO] Requesting user authentication via browser
	[2017-10-05 08:51:37.053] [42968] [DEBUG] Starting HTTP server
	[2017-10-05 08:51:43.444] [42968] [DEBUG] Received HTTP request: GET /?code=4/Nd2rioLCh20PgBHML6vBUYacMCddkRpl0s2U4HR2GrW HTTP/1.1
	[2017-10-05 08:51:43.709] [42968]  [INFO] Refresh token added to keychain
	[2017-10-05 08:51:43.765] [42968]  [INFO] Access token added to keychain, expires in 3600 seconds
	[2017-10-05 08:51:43.765] [42968] [DEBUG] Stopping HTTP server
	[2017-10-05 08:51:44.804] [42968]  [INFO] Got 155 items from Google Drive
	[2017-10-05 08:51:44.815] [42968] [DEBUG] Execution took 7.814 seconds
	[2017-10-05 08:51:44.985] [42983] [DEBUG] ./google-drive.rb ["--filter", "foo"]
	[2017-10-05 08:51:44.988] [42983] [DEBUG] Loaded 155 items from cache (created 8 seconds ago)
	[2017-10-05 08:51:44.989] [42983] [DEBUG] Execution took 0.003 seconds
	```

## Supported Files Types

- Google Docs
- Google Sheets
- Google Slides
- Google Forms
- PDFs

## Developers

1. Download this repository:

		git clone --recursive https://github.com/azai91/alfred-drive-workflow

2. Create a blank workflow

3. Create a symbolic link making the new blank workflow point to the `src` folder of this repository (find the blank workflow by right clicking it in Alfred and select `Open in Terminal/Finder`)

## Demo

![Search Google Drive from Alfred using the Google Drive workflow](./assets/search.gif)

![Create a document from Alfred using the Google Drive workflow](./assets/create.gif)
