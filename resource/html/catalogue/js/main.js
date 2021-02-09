$(document).ready(function() {
  new QWebChannel(qt.webChannelTransport, function(channel) {
    // get qt interact object
    var interactObj = channel.objects.interactObj;
    $('#get_catalogue').click(function () {
      interactObj.get_tree();
    });
    interactObj.SigSendMessageToJS.connect(function(str) {
      //$('#result').html(JSON.parse(str))
      list_json = JSON.parse(str);
      var ss = '';
      for(var i in list_json) {
        ss += list_json[i].name;
      }
      alert(ss);
    })
  }) 
});
