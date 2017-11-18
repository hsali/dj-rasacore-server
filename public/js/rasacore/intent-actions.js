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
    props: ['intent'],
    data: function(){
        return {
            actions: [],
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
                self.actions = res.results;
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