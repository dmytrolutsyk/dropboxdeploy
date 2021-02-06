#!/usr/local/bin/python3

import os
import argparse
import requests
import json
import re
import dropbox

def dropbox_upload(target_file_name, source_file, dropbox_token, dropbox_folder):
    dropbox_path = '/{folder}/{file_name}'.format(folder=dropbox_folder, file_name=target_file_name)
    dbx = dropbox.Dropbox(dropbox_token)
    data=open(source_file, 'rb')
    dbx.files_upload(data.read(), "/app.apk", files.WriteMode.update)


def get_app(release_dir):
    output_path = os.path.join(release_dir, 'output-metadata.json')

    with(open(output_path)) as app_output:
        json_data = json.load(app_output)

    print(json_data)
    apk_details_key = ''
    if 'elements' in json_data:
        apk_details_key = json_data['elements']
    else:
        print("Failed: parsing json in output file")
        return None, None

    app_version = apk_details_key[0]['versionName']
    app_file = os.path.join(release_dir, apk_details_key[0]['outputFile'])
    print(app_file, app_version)
    return app_version, app_file


def get_target_file_name(app_name, app_version):
    app_name = app_name.lower()
    app_version = app_version.replace('.', '_')
    return '{name}_{version}.apk'.format(name=app_name, version=app_version).replace(' ','')



if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--release.dir', dest='release_dir', help='path to release folder', required=True)
    parser.add_argument('--app.name', dest='app_name', help='app name that will be used as file name', required=True)
    parser.add_argument('--dropbox.token', dest='dropbox_token', help='dropbox access token', required=True)
    parser.add_argument('--dropbox.folder', dest='dropbox_folder', help='dropbox target folder', required=True)

    options = parser.parse_args()

    # Extract app version and file
    app_version, app_file = get_app(options.release_dir)
    if app_version == None or app_file == None:
        exit(OUTPUT_FILE_PARSING_ERROR)

    target_app_file = get_target_file_name(options.app_name, app_version)

    # Upload app file and get shared url
    dropbox_upload(target_app_file, app_file, options.dropbox_token, options.dropbox_folder)
