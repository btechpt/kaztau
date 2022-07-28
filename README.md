# Kaztau

Kaztau is a simple cli app to send message telegram. Just call command on shell or execute via cron for create reminder notification.

### Installation
```shell
pip install kaztau
```
export your telegram credential
```shell
export KAZTAU_TELEGRAM_API_ID=112233
export KAZTAU_TELEGRAM_API_HASH='11aaa22bb'
export KAZTAU_TELEGRAM_BOT_TOKEN='22bb33cc'
```

export your whatsapp device_id
```shell
export WA_DEVICE_ID="a012asdf09123"
```
on this package author use whatsapp api from [whacenter.com](https://whacenter.com/)

### How to use

#### Send Whatsapp Message
- Send message run command 
  ```shell
  kaztau send_wa_message "{identifier}" "{your_message}"
  ````
  Example:
  ```shell
  kaztau send_wa_message "628998123123" "Test send message from kaztau"
  ```
  
#### Send Whatsapp Image
- Send image run command 
  ```shell
  kaztau send_wa_image "{identifier}" "{your_message}" "{image_path}"
  ```
  Example:
  ```shell
  kaztau send_wa_image "628998123123" "New Picture" "/Users/Userexam/Pictures/image_report.png"
  ```

#### Send Whatsapp Multi Images
- Send images run command 
  ```shell
  kaztau send_wa_mult_image "{identifier}" "{your_message"} --path-file "{path_file_1}" --path-file "{path_file_2}"
  ```
  Example:
  ```shell
  kaztau send_wa_multi_image "628998123123" "Multi Picture" --path-file "/Users/Userexam/Pictures/image_report_1.png" --path-file "/Users/userexam/Pictures/image_report_2.png"
  ```
  Alternative argument you can use `--path-folder` to send all image in the folder
  ```shell
  kaztau send_wa_multi_image "628998123123" "Multi Picture" --path-folder "/Users/Userexam/Pictures/dir_images"
  ```
  
#### Send Whatsapp Images Option Arg
If you want to send image and move image to another folder after success, you can use this option
- Move image to another directory after success `send_wa_image` or `send_wa_multi_image`. 
  
  You can add argument `--move-path {move_path}`. Example on `send_image`
  ```shell
  kaztau send_wa_image "628998123123" "New Pictures" --path-file "/Users/Userexam/Pictures/image_report.png" --move-folder "/Users/Userexam/Pictures/success"
  ```
  Example on `send_wa_multi_image`
  ```shell
  kaztau send_wa_multi_image "628998123123" "Multi Picture" --path-file "/Users/Userexam/Pictures/image_report_1.png" --path-file "/Users/userexam/Pictures/image_report_2.png" --move-folder "/Users/Userexam/Pictures/success"
  ```
  or 
  ```shell
  kaztau send_wa_multi_image "628998123123" "Multi Picture" --path-folder "/Users/Userexam/Pictures/dir_images" --move-folder "/Users/Userexam/Pictures/success"
  ```
  
#### Send Whatsapp Message or Images to group
If you want to send message, image or multi image, you just change `{identifier}` from `number` to `group name` and add option `--togroup`, Example:
  ```shell
  kaztau send_wa_message "Dev Python" "Test send message from kaztau" --togroup
  ```
  ```shell
  kaztau send_wa_multi_image "Dev Python" "Multi Picture" --path-folder "/Users/Userexam/Pictures/dir_images" --move-folder "/Users/Userexam/Pictures/success" --togroup
  ```
