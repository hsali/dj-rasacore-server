const userSaysTemplateStr = `
    <div class="tabular-list">
        <table class="table table-bordered table-condensed table-hover">
            <tbody>
                <tr v-for="user_say in user_says">
                    <td class="col-md-11">
                        <input type="text" v-model="user_say.name" placeholder="User example text" class="form-control input-sm">
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
    props: ['intent'],
    template: userSaysTemplateStr,
    data: function() {
        return {
            user_says: [],
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
                self.user_says = res.results;
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