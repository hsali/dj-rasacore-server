var Training = new Vue({
    el: "#trainingContainer",
    data: function() {
        return {
            story: null,
            intent: null,
            intents: [],
            stories: [],
            usersays: [],
            actions: [],
            pagination: {
                count: 0,
                next: false,
                prev: false
            },
            // Handle modals
            show_add_story_modal: false,
            show_add_intent_modal: false,
            show_add_example_modal: false,
            show_add_action_modal: false
        }
    },
    watch: {
        'story': function() {
            this.intent = null;
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
        },
        showAddStoryModal: function(){
            this.show_add_story_modal = true
        },
        showAddIntentModal: function(){
            this.show_add_intent_modal = true
        },
        showAddExampleModal: function(){
            this.show_add_example_modal = true
        },
        showAddActionModal: function(){
            this.show_add_action_modal = true
        }
    }
})