var sectionHeaderTemp = `
    <h4>{{title}}
        <span class="action">
            <button class="btn btn-primary btn-xs" @click="btnClickAction()">
                <i class="fa fa-plus-circle"></i> {{btnlabel}}
            </button>
        </span>
    </h4>
`;

Vue.component('sectionHeader', {
template: sectionHeaderTemp,
props: ['title', 'btnlabel', 'btnaction'],
methods: {
    btnClickAction: function()   {
        this.btnaction();
    }
}
});