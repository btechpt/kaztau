# Kaztau

Kaztau is a simple cli app to send message telegram. Just call command on shell or execute via cron for create reminder notification.

### Installation
```shell
pip install ....
```
export your telegram credential
```shell
export KAZTAU_TELEGRAM_API_ID=112233
export KAZTAU_TELEGRAM_API_HASH='11aaa22bb'
export KAZTAU_TELEGRAM_BOT_TOKEN='22bb33cc'
```

### How to use
#### Management data group chat
- Add data group run command 
  ```shell
  kaztau add {group_id} --name "{group_name}"
  ```
  Example:
  ```shell
  kaztau add groupexample --name "Group Example" 
  ```
- Show all data group, run command
  ```shell
  kaztau list
  ```
  You can see all data
  ```shell
  Group list:

  ID.  | Group ID  | Verify  | Name  
  -----------------------------------
  1    | (groupexample)| False   | Group Example
  -----------------------------------
  ```
- Remove group, run command `kaztau remove {data_id}`. Example
  ```shell
  kaztau remove 1
  ```

#### Send Message
- Send message to group run command 
  ```shell
  kaztau send_message {data_id} --message "{your_message}"
  ````
  Example:
  ```shell
  kaztau send_message 1 --message "Test send message from kaztau"
  ```
- Send image to group run command 
  ```shell
  kaztau send_image {data_id} --path-file "{path_file}"
  ```
  Example:
  ```shell
  kaztau send_image 1 --path-file "/Users/Userexam/Pictures/image_report.png"
  ```
- Send multi image to group run command 
  ```shell
  kaztau send_image {data_id} --path-file "{path_file_1}" --path-file "{path_file_2}"
  ```
  Example:
  ```shell
  kaztau send_multi_image 1 --path-file "/Users/Userexam/Pictures/image_report_1.png" --path-file "/Users/userexam/Pictures/image_report_2.png"
  ```
  Alternative argument you can use `--path-folder` to send all image in the folder
  ```shell
  kaztau send_multi_image 1 --path-folder "/Users/Userexam/Pictures/dir_images"
  ```
- Move image to another directory after success `send_image` or `send_multi_image`. 
  
  You can add argument `--move-path {move_path}`. Example on `send_image`
  ```shell
  kaztau send_image 1 --path-file "/Users/Userexam/Pictures/image_report.png" --move-folder "/Users/Userexam/Pictures/success"
  ```
  Example on `send_multi_image`
  ```shell
  kaztau send_multi_image 1 --path-file "/Users/Userexam/Pictures/image_report_1.png" --path-file "/Users/userexam/Pictures/image_report_2.png" --move-folder "/Users/Userexam/Pictures/success"
  ```
  or 
  ```shell
  kaztau send_multi_image 1 --path-folder "/Users/Userexam/Pictures/dir_images" --move-folder "/Users/Userexam/Pictures/success"
  ```