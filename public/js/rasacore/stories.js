var storyListTemp = `
    <ul class="list-unstyled component-list">
        <li v-for="story in stories" @click="openStory(story.id)">
            <a href="javascript:;">{{story.title}}</a>
        </li>
    </ul>`;

Vue.component('storyList', {
    props: ['stories', 'story'],
    template: storyListTemp,
    methods: {
        openStory: function(id) {
            this.$emit('update:story', id)
        }
    }
});

var addStoryModalTemp = `
    <modal v-model="show_modal" @ok="saveForm" @cancel="cancelAction">
        <div slot="modal-header" class="modal-header">
            <h4 class="modal-title">New Story</h4>
        </div>
        <div slot="modal-body" class="modal-body">
            <form>
                <div class="form-group">
                    <label class="control-label">Title</label>
                    <input type="text" class="form-control" v-model="form.title" name="title" required>
                </div>
            </form>
        </div>
    </modal>
    </span>
`;

Vue.component('addStory', {
    template: addStoryModalTemp,
    props: ['start', 'story', 'stories'],
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
                title: ''
            }
        }
    },
    methods: {
        saveForm: function() {
            var self = this;
            App.showProcessing()
            App.remotePost('/api/v1.0/stories/', self.form, 
            function(res){
                self.show_modal = false;
                // Update stories
                var stories = self.stories;
                stories.unshift(res);
                self.$emit('update:stories', stories);
                self.$emit('update:story', res.id);
                // Reset form
                self.form.title = '';
                // Close modal
                self.$emit('update:start', false);
                App.hideProcessing()
            }, function(err){
                App.notifyUser(err, "error");
                App.hideProcessing()
            });
            
        },
        cancelAction: function() {
            this.show_modal = false;
            this.$emit('update:start', false);
        }
    }
});