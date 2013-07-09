LHSPNservice
============

LHS Push Notification service is a module for sending push notifications (currently only to iOS) using Python.

There are plans to extend this to allow push notifications to be sent to other platforms with the same system.

## APNservice

**NOTE**: To work with and use push notifications with Apple devices you will need a Apple developer licence for ether iOS or OS X. Go to: [https://developer.apple.com/programs/](https://developer.apple.com/programs/) for more information.

### Registering and Saving Tokens for Push Notifications
The module `DeviceTokenHandler.py` will deal with connecting to a MySQL database and dealing with all the information. This module is still under construction however and will be added soon.

For reference a database to store this information should allow you to save at least the following variables:  
• Device Token (string)  
• Badge Number (unsigned int)  
• Last Updated (timestamp)  

### Creating Certificates
For information on creating APNs certificates please refer to the [Apple documents](http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ProvisioningDevelopment.html).

### Creating and Sending Notifications
To create and send notifications to a device or series of devices please use the following steps:

1. Call `makeAlert(body, actionLocKey, locKey, locArgs, launchImage):` to create a alert dictionary.  

2. Then create an instance of `APNservice` class.  

3. Queue the notifications with `APNservice.queueNotifications(tokens, alert, sound):`. If you just want to send the alert to one device then just make `tokensArray` contain one device token.  

4. LHS will send your notification to all tokens.  

##### Example Code

```
tokensArray = ["19e5d3a4a27eb08e9b2d22166152a5492fd645868f1e6909e80ba99256c8590f", "27788ada507d3ea5e0f7a01b2305f7ffe9a116b03a22677dfe765771fdc28148"]
alertDict = makeAlert("This is a test Push Notification!", None, None, None, None)  

pushService = APNservice()  
pushService.queueNotifications(tokensArray, alertDict, None)
```

### How LHS Sends Notifications

LHS uses a queuing system to send push notifications. This is because Apple does not return a response when a notification has been sent, and also because a returned error can be received after more notifications have already been sent. The following outlines the process used for queuing and sending notifications:

1. All notifications are created and packed into binary form. As they are created they are assigned an ID incrementing from `0`.

2. Each binary is stored in the `notifBinaryDict` dictionary with its ID being the key.

3. The `queueIDsList` list is then populated with the keys of `notifBinaryDict`, opens a socket and begins to send the notifications after starting an asynchronous thread reading from the socket.

4. After a notification has been sent its ID gets put in the `sentIDsList` list.

5. If an error is read from the socket, sending is stopped. Every ID in the `sentIDsList` that was sent after the failed notification gets put back at the front of the `queueIDsList` list to send again.

6. The sending is then restarted, opening a new socket.

7. When all notifications are sent the socket is closed, the ID count reset to `0` and the reading thread is stopped.

The failed notification is logged with its ID and error status. If it is due to error status 1 or 10 then it tries to resend. If a notification reaches its retry count then it is logged and removed from the queue. For more information of error status codes check the [Apple documents](http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/CommunicatingWIthAPS.html).

For more information on this method of sending push notifications please read this blog about it: [The Problem With Apples Push Notification Service... Solutions and Workarounds...](http://redth.info/the-problem-with-apples-push-notification-ser/)

### Checking the Feedback Service

Apple recommends checking the feedback service to remove any device tokens from your database that are no longer active. To read more about this check out the [Apple documents](http://developer.apple.com/library/mac/#documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/CommunicatingWIthAPS.html).

To do this with LHS, create an instance of APNservice and call the `APNservice.checkFeedbackService():` method, which returns an array of tuples containing:  
[0] Unix timestamp  
[1] Token length  
[2] Token

These are device tokens that are no longer valid along with a timestamp of when that token was invalidated. You should remove these from your data of tokens since these devices have uninstalled your app and can no longer receive notifications.

**NOTE**: It is recomended to check the timestamp from when the token was invalidated to the last updated timestamp in your database, incase the user has re-installed the app between the invalidation and your check.

##### Example Code

```
pushService = APNservice()  
invalidTokens = pushService.checkFeedbackService()
print invalidTokens
>> [(1373042568, 32, '19e5d3a4a27eb08e9b2d22166152a5492fd645868f1e6909e80ba99256c8590f'), (1373042568, 32, '27788ada507d3ea5e0f7a01b2305f7ffe9a116b03a22677dfe765771fdc28148')]
```  

## License

LHServer is available under the MIT license. See the LICENSE file for more info.

### Creator

[James Barrow - Pig on a Hill](http://pigonahill.com)  
[@PigonaHill](https://twitter.com/PigonaHill)
