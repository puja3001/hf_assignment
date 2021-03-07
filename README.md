Weekly Menu Manager
====================================

Weekly-Menu manager is single point of contact for all notifications registrations and notifications subscriptions.
That means it helps user/device level control and business flow level control.


Data flow:
===========

1. Use has to register device by using user-subscriptions in order for AWS pinpoint to push the messages to Notification network(for mobile), email hosts(email), websocket(socketio). This gives high level control(user / device level)

2.  User can control the business flows using businessflow subscriptions.This means suppose you want to subscribe to FEEDS on your mobile device, from your device you can enable/disable a particular feed.This is very finer control.for eg, if usre wants to receive feed1, feed2,feed3 but not feed4.User can just enable feed1, feed2,feed3 and disable feed4.

Concepts:
=========
ALl the APIs are primarily have below concepts:

1. **user_id**: Either it can be passed as parameter and also can be made available from JWT token

2. **token_id**: It is uniquely identifiable with user,for eg, can be device token, email, webtoken, mobile num

3. **business_flow**: Flow is nothing but products/features. Primarily we have we have 3 business flows **"feeds", "personal_folders", "peak_alerts"**.
4. **flow_id**: This help is finer control of subscribing/unsubscribing to a flow. eg : save_search_id
5. **type**:  We support **"mobile", "email", "web", "sms"**
6. **subtype**: We support **"android", "ios"** for mobile and for the rest subtype is defaulted to type.


API design:
===========
Endpoints and its major responsibilities below.
1. User subscriptions
    - registering device
    - unregistering device
2. Business flows
    - enabling a particular flow id under flow
    - disabling a particular flow id under flow
3. Templates
    - customized templates for a token_id, type and subtype combinations
    - For eg : This may not be applicable for mobile, but for email, you can store whole email template here.
4. Notification logs
    - This is to log all the notifications sent
5. Actions
     - It will get all enabled user subscriptions and templates

To run locally:

```
1. Start a local instance of postgres server
2. Create tables and add test data - python setup.py
3. Run the command - env ENV=dev python app.py'
```

Or with docker:

```
1. docker build -t weekly-menu-manager .
2. docker run -p 8080:8080 -e ENV=dev weekly-menu-manager
```

Unit testing:
==============
