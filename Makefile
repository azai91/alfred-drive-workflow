default:
	echo "No default rule."

Google-Drive.alfredworkflow: src/google-drive.rb src/info.plist src/icon.png src/icons
	cd src && zip -r ../$@ *

tag:
	git tag -a "v$$(<src/version)" --message "Release tag for version $$(<src/version)" --sign

.PHONY: default tag
