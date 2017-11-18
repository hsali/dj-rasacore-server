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