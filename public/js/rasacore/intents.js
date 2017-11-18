var intentsListTemp = `
<ul class="list-unstyled component-list">
    <li v-for="item in intents" @click="openIntent(item.id)" v-bind:class="{'active': (item.id==intent)}">
        <a href="javascript:;">{{item.name}}</a>
    </li>
</ul>`;

Vue.component('intentsList', {
    template: intentsListTemp,
    props: ['story', 'intent', 'intents'],
    data: function(){
        return {
            pagination: {
                count: 0,
                next: false,
                prev: false
            }
        }
    },
    watch: {
        'story': function(newVal, oldVal) {
            this.getStoryIntents(newVal);
        }
    },
    methods: {
        getStoryIntents: function(story_id) {
            var self = this;
            App.showProcessing()
            App.remoteGet('/api/v1.0/intents/?story='+story_id, {}, 
            function(res){
                self.$emit('update:intents', res.results);
                self.pagination.count = res.count;
                self.pagination.next = res.next;
                self.pagination.previous = res.previous;
                App.hideProcessing()
            }, function(err){
                App.notifyUser(err, "error");
                App.hideProcessing()
            });   
        },
        openIntent: function(id) {
            this.$emit('update:intent', id)
        }
    }
});


var addIntentModalTemp = `
<modal v-model="show_modal" @ok="saveForm" @cancel="cancelAction">
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">New Intent</h4>
    </div>
    <div slot="modal-body" class="modal-body">
        <form>
            <div class="form-group">
                <label class="control-label">Name</label>
                <input type="text" class="form-control" v-model="form.name" name="name" required>
            </div>
        </form>
    </div>
</modal>
</span>
`;

Vue.component('addIntent', {
    template: addIntentModalTemp,
    props: ['start', 'story', 'intent', 'intents'],
    components: {
        modal: VueStrap.modal
    },
    watch: {
        'start': function(newVal, oldVal) {
            this.show_modal = newVal;
        }
    },
    data: function(){
        return {
            show_modal: false,
            form: {
                name: '',
                story: null
            }
        }
    },
    methods: {
        saveForm: function() {
            var self = this;
            self.form['story'] = this.story;
            App.showProcessing()
            App.remotePost('/api/v1.0/intents/', self.form, 
            function(res){
                self.show_modal = false;
                // Update intents
                var intents = self.intents;
                intents.unshift(res);
                self.$emit('update:intents', intents);
                self.$emit('update:intent', res.id);
                // Reset form
                self.form.name = '';
                // Close modal
                self.$emit('update:start', false);
                App.hideProcessing();
                App.notifyUser('Intent added');
            }, function(err){
                App.notifyUser(err.responseText, "error");
                App.hideProcessing();
            });
            
        },
        cancelAction: function() {
            this.show_modal = false;
            this.$emit('update:start', false);
        }
    }
});