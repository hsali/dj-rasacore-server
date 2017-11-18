var Training = new Vue({
    el: "#trainingContainer",
    data: function() {
        return {
            story: null,
            intent: null,
            stories: [],
            pagination: {
                count: 0,
                next: false,
                prev: false
            }
        }
    },
    created: function() {
        this.getStories();
    },
    methods: {
        getStories: function() {
            var self = this;

            App.showProcessing()
            App.remoteGet('/api/v1.0/stories/', {}, 
            function(res){
                self.stories = res.results;
                self.pagination.count = res.count;
                self.pagination.next = res.next;
                self.pagination.previous = res.previous;
                App.hideProcessing()
            }, function(err){
                App.notifyUser(err, "error");
                App.hideProcessing()
            });
        }
    }
})