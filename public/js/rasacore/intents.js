var intentsListTemp = `
<ul class="list-unstyled component-list">
    <li v-for="intent in intents">
        <a href="javascript:;">{{intent.name}}</a>
    </li>
</ul>`;

Vue.component('intentsList', {
    template: intentsListTemp,
    props: ['story'],
    data: function(){
        return {
            intents: [],
            pagination: {
                count: 0,
                next: false,
                prev: false
            }
        }
    },
    watch: {
        'story': function(newVal, oldVal) {
            console.log('Active story', newVal);
            this.getStoryIntents(newVal);
        }
    },
    methods: {
        getStoryIntents: function(story_id) {
            var self = this;
            App.showProcessing()
            App.remoteGet('/api/v1.0/intents/?story='+story_id, {}, 
            function(res){
                self.intents = res.results;
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
});