<script>
    import dayjs from 'dayjs';
    import {goto, url} from '@roxi/routify'
    import Card from "./card/Card.svelte";
    import Content from "./card/Content.svelte";

    export let journal = {};

    function displayDiff(value) {
        if (value === '' || value === null || value === undefined) {
            return ''
        }
        let str = '';
        if (value >= 3600) {
            const hours = Math.floor(value / 3600)
            const left = value - hours * 3600;
            str += hours + 'h';
            value = left;
        }
        if (value >= 60) {
            const minutes = Math.floor(value / 60)
            const left = value - minutes * 60;
            str += minutes + 'm';
            value = left
        }
        if (value > 0) {
            if (str === '') {
                str = value.toFixed(2) + 's'
            } else if (value >= 1) {
                str += value.toFixed(0) + 's'
            }
        }

        return str;
    }

    function openJournal() {
        // not working
        $goto('/journal/:journal', {journal: journal.id})
    }

    $:status = (journal.finishedAt ? (journal.error ? 'failed' : 'success') : 'pending')
    $:startedAt = dayjs(journal.startedAt)
</script>

<Card>
    <a href="/journal/:journal" use:$url={{journal: journal.id}} style="text-decoration: none">
        <!-- FIXME: workaround due to bug in GoTo -->
        <Content status="{status}" title={journal.operation} tip="#{journal.id}">
            {journal.description}
            <span slot="footer">{startedAt.format('DD MMMM YYYY')}</span>
            <span slot="footer">{displayDiff(journal.duration)}</span>
            <span slot="footer">{startedAt.format('HH:mm:ss')}</span>
        </Content>
    </a>
</Card>