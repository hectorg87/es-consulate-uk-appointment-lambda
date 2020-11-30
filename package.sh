rm function.zip
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip appointments.py
aws --profile uk lambda update-function-code --function-name consulateAppointment --zip-file fileb://function.zip
