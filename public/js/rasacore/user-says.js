const userSaysTemplateStr = `
    <div class="tabular-list">
        <table class="table table-bordered table-condensed table-hover">
            <tbody>
                <tr v-for="usersay in usersays">
                    <td class="col-md-11">
                        <input type="text" v-model="usersay.text" placeholder="User example text" class="form-control input-sm">
                    </td>
                    <td>
                        <button class="btn btn-neutral btn-sm">
                            <i class="fa fa-plus"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>`;
    
Vue.component('userSays', {
    props: ['intent', 'usersays'],
    template: userSaysTemplateStr,
    data: function() {
        return {
            pagination: {
                count: 0,
                next: false,
                prev: false
            }
        }
    },
    watch: {
        'intent': function(newVal, oldVal) {
            this.getUserSays(newVal);
        }
    },
    methods: {
        getUserSays: function(intent_id) {
            var self = this;
            App.showProcessing()
            App.remoteGet('/api/v1.0/user-says/?intent='+intent_id, {}, 
            function(res){
                self.$emit('update:usersays', res.results);
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


var addUserSayModalTemp = `
<modal v-model="show_modal" @ok="saveForm" @cancel="cancelAction">
    <div slot="modal-header" class="modal-header">
        <h4 class="modal-title">New User Say Example</h4>
    </div>
    <div slot="modal-body" class="modal-body">
        <form>
            <div class="form-group">
                <label class="control-label">Text</label>
                <input type="text" class="form-control" v-model="form.text" name="name" required>
            </div>
        </form>
    </div>
</modal>
</span>
`;

Vue.component('addUsersay', {
    template: addUserSayModalTemp,
    props: ['start', 'intent', 'usersays'],
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
                text: '',
                intent: null
            }
        }
    },
    methods: {
        saveForm: function() {
            var self = this;
            self.form['intent'] = this.intent;
            App.showProcessing()
            App.remotePost('/api/v1.0/user-says/', self.form, 
            function(res){
                self.show_modal = false;
                // Update user says
                var usersays = self.usersays;
                usersays.unshift(res);
                self.$emit('update:usersays', usersays);
                // Reset form
                self.form.text = '';
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