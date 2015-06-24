// snippet to add to your global js for parent-side iframe resizing.

window.addEventListener('message', handleMessage, false);

function handleMessage(e) {
  if (e.data && e.data.request === 'changeHeight') {
    var iframe = findIframe(e.data.href);
    if (iframe) {
      iframe.height = e.source.document.body.scrollHeight;
    }
    else {
      console.log('Could not find iframe with href', e.data.href);
    }
  }
}

function findIframe(href) {
  var iframes = document.querySelectorAll('iframe');
  for (var i = 0; i < iframes.length; ++i) {
    var iframe = iframes[i];
    if (iframe.src === href) {
      return iframe;
    }
  }
}