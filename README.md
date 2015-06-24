
A Harvard-specific Django LTI app that allows course authors to insert a 
"course information" widget containing live-updated course information from the registrar into 
any page with a rich content editor.

It replaces functionality formerly provided by isites.

Authors click an icon, which opens a widget editor window to let them choose
which fields they would like to include in the widget. The widget is then 
inserted into the page, and is live-updated using the icommons api.

In order for the iframes to resize properly, you'll have to add the following
snippet to your canvas global js file:

course_info/static/js/consumer/global.js

Set log to false once you're satisfied it's working (will emit lots of messages to js console). 

See the docs directory for instructions on how to run locally and in heroku.