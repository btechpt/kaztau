# Kaztau

Kaztau is a simple cli app to send message telegram. Just call command on shell or execute via cron for create reminder notification.

### Instalation
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
- Add data group run command `kaztau add {group_id} --name "{group_name}"`. Example:
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
- Send message to group run command `kaztau send_message {data_id} --message "{your_message}"`. Example:
  ```shell
  kaztau send_message 1 --message "Test send message from kaztau"
  ```
- Send image to group run command `kaztau send_image {data_id} --path-file "{path_file}"`
  ```shell
  kaztau send_image 1 --path-file "/Users/userexam/Pictures/image_report.png"
  ```
- Send multi image to group run command `kaztau send_image {data_id} --path-file "{path_file_1}" --path-file "{path_file_2}"`
  ```shell
  kaztau send_multi_image 1 --path-file "/Users/userexam/Pictures/image_report_1.png" --path-file "/Users/userexam/Pictures/image_report_2.png"
  ```
- Remove group, run command `kaztau remove {data_id}`. Example
  ```shell
  kaztau remove 1
  ```