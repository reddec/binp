<script>
    import dayjs from 'dayjs';
    import {url} from '@roxi/routify'
    export let journal = {};

    function displayDiff(value) {
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

    $:status = (journal.finishedAt ? (journal.error ? 'failed' : 'success') : 'pending')
    $:startedAt = dayjs(journal.startedAt)
</script>
<style>
    .card {
        min-height: 3em;
        display: flex;
        flex-direction: row;
        cursor: pointer;
        flex-grow: 1;
        align-items: stretch;
        text-decoration: none;
        color: black;
    }

    .info {
        flex-grow: 1;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        padding: 0.5em;
        background-color: white;
    }

    .tong {
        text-orientation: sideways;
        writing-mode: vertical-rl;
        text-align: center;
        padding: 0.2em 0.2em 0.2em 1em;
        color: white;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        z-index: -1;
        margin-left: -1em;
        text-transform: uppercase;
    }

    .head {
        display: flex;
        justify-content: space-between;
    }

    .title {
        align-self: center;
        font-size: large;
    }

    .footer {
        display: flex;
        justify-content: space-between;
        font-size: x-small;
    }

    .body {
        padding-top: 1.2em;
        padding-bottom: 1.2em;
        font-size: smaller;
        color: #666666;
    }

    .muted {
        align-self: center;
        color: #999999;
    }

    .id {
        font-size: smaller;
    }

    .success {
        background-color: #79c21b;
        color: white;
    }

    .pending {
        background-color: white;
        color: black;
    }

    .failed {
        background-color: #F24726;
        color: white;
    }
</style>
<a href="/journal/:journalId" use:$url={{journalId:journal.id}} class="card">
    <div class="info">
        <div class="head">
            <span class="title">{journal.operation}</span>
            <span class="muted id">#{journal.id}</span>
        </div>
        <div class="body">
            {journal.description}
        </div>
        <div class="footer">
            <span class="muted">{startedAt.format('DD MMMM YYYY')}</span>
            {#if journal.duration}
                <span class="muted">{displayDiff(journal.duration)}</span>
            {/if}
            <span class="muted">{startedAt.format('HH:mm:ss')}</span>
        </div>
    </div>
    <div class="tong {status}">
        <span>{status}</span>
    </div>
</a>
