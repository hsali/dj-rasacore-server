var actionsListTemp = `
    <div>
        <div class="group" v-for="action in actions">
            <h3>{{action.name}}</h3>
            <div>
                {{action}}
            </div>
        </div>
    </div>`;

Vue.component('actionsList', {
    template: actionsListTemp,
    props: ['intent', 'actions'],
    data: function(){
        return {
            pagination: {
                count: 0,
                next: false,
                prev: false
            }
        }
    },
    created: function() {
        this.initComponent();
    },
    watch: {
        'intent': function(newVal, oldVal) {
            this.getIntentActions(newVal);
        }
    },
    methods: {
        getIntentActions: function(intent_id) {
            var self = this;
            App.showProcessing()
            App.remoteGet('/api/v1.0/intent-actions/?intent='+intent_id, {}, 
            function(res){
                self.$emit('update:actions', res.results);
                self.pagination.count = res.count;
                self.pagination.next = res.next;
                self.pagination.previous = res.previous;
                App.hideProcessing();

                $(self.$el).accordion( "refresh" );
            }, function(err){
                App.notifyUser(err, "error");
                App.hideProcessing()
            });   
        },
        initComponent: function() {
            var self = this;
            $(function() {
                $(self.$el).accordion({
                    header: "> div > h3"
                }).sortable({
                    axis: "y",
                    handle: "h3",
                    stop: function( event, ui ) {
                        // IE doesn't register the blur when sorting
                        // so trigger focusout handlers to remove .ui-state-focus
                        ui.item.children( "h3" ).triggerHandler( "focusout" );
                        // Refresh accordion to handle new order
                        $(self.$el).accordion( "refresh" );
                    }
                });
            });
        }
    }
});

var addActionModalTemp = `
<modal v-model="show_modal" @ok="saveForm" @cancel="cancelAction">
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">Add Action</h4>
    </div>
    <div slot="modal-body" class="modal-body">
        <form>
            <div class="form-group">
                <label class="control-label">Text</label>
                <select class="form-control" v-model="form.action" required>
                    <option value="17">17</option>
                    <option value="18">18</option>
                </select>
            </div>
        </form>
    </div>
</modal>
</span>
`;

Vue.component('addAction', {
    template: addActionModalTemp,
    props: ['start', 'intent', 'actions'],
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
                action: null,
                intent: null
            }
        }
    },
    methods: {
        saveForm: function() {
            var self = this;
            self.form['intent'] = this.intent;
            App.showProcessing()
            App.remotePost('/api/v1.0/intent-actions/', self.form, 
            function(res){
                self.show_modal = false;
                // Update user says
                var actions = self.actions;
                actions.unshift(res);
                self.$emit('update:actions', actions);
                // Reset form
                self.form.action = '';
                // Close modal
                self.$emit('update:start', false);
                App.hideProcessing();
                App.notifyUser('Action added');
            }, function(err){
                App.notifyUser(err.responseText, "error");
                App.hideProcessing()
            });
            
        },
        cancelAction: function() {
            this.show_modal = false;
            this.$emit('update:start', false);
        }
    }
});