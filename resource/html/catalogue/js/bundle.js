var app = new Vue({
  el: '#app',
  data: {
    interactObj: null,
    list: [],
    current: null,
    show: null,
    text: '',
    isdir: true
  },
  mounted() {
    var that = this;
    new QWebChannel(qt.webChannelTransport, function(channel) {
      that.interactObj = channel.objects.interactObj;
      that.interactObj.SigSendMessageToJS.connect(function(str) {
        that.list = JSON.parse(str);
      });
      that.interactObj.get_tree();
    });
  },
  methods: {
    getTree: function() {
      if(this.interactObj) {
        this.interactObj.get_tree();
      }
    },
    deleteFile: function(item) {
      this.interactObj.delete_file(item.name, item.dir);
    },
    addFile: function(item) {
      this.show = item.name;
      this.isdir = false;
    },
    addCatalogue: function(item) {
      this.show = item.name;
      this.isdir = true;
    },
    addConfirm: function(item) {
      if(this.show != null) {
        if(this.isdir) {
          this.interactObj.add_catalogue(this.text, item.dir, item.name);
        } else {
          this.interactObj.add_file(this.text, item.dir, item.name);
        }
        this.show = null;
      }
    },
    editFile: function(item) {
      this.show = item.name;
      this.text = item.name;
    },
    editFileConfirm: function(item) {
      if(this.show != null) {
        this.interactObj.rename_file(item.name, this.text, item.dir);
        this.show = null;
      }
    },
    updateEdit: function(item) {
      this.current = item.name;
      this.interactObj.update_edit(item.name, item.dir);
    }
  }
})
