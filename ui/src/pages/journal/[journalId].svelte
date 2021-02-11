<!-- routify:options title="Journal" -->
<!-- routify-options param-is-page -->
<script lang="ts">
    import {metatags} from '@roxi/routify'
    import JournalCard from "../../_components/JournalCard.svelte";
    import {InternalAPI} from "../../api";
    import {onDestroy, onMount} from "svelte";
    import Loader from "../../_components/Loader.svelte";
    import RecordCard from "../../_components/RecordCard.svelte";
    import Callout from "../../_components/Callout.svelte";
    import {journalUpdates, Updates} from "../../api/updates";
    import {Journal} from "../../api/internal";
    import {fade} from 'svelte/transition'

    export let journalId;

    let journal: Journal;

    let failedMessage;
    let downloading = true;
    let updates: Updates<Journal> = null;

    metatags.title = `Journal ${journalId}`

    async function download() {
        downloading = true;
        failedMessage = null;
        try {
            journal = await InternalAPI.getJournal({journalId: journalId});
        } catch (e) {
            failedMessage = e.toString();
        } finally {
            downloading = false;
        }
    }

    function init() {
        download();
        updates = journalUpdates(journalId, update);
    }

    function update(updatedJournal: Journal) {
        journal = updatedJournal;
    }

    onMount(init);
    onDestroy(() => updates.close())

</script>
<style>
    .list {
        width: 100%;
        max-width: 50em;
        align-self: center;
        display: flex;
        justify-content: stretch;
        flex-direction: column;
    }

    .content {
        margin-top: 1em;
        display: flex;
        justify-content: stretch;
        flex-direction: column;
        padding: 0.5em;
    }

    hr {
        margin-top: 1em;
        margin-bottom: 1em;
        width: 100%;
        border-top: dashed #999999 thin;
    }

    .records-header {
        margin: 0;
        color: #999999;
        font-size: x-large;
        text-align: center;
    }

</style>
<div class="content">
    <div class="list">
        {#if downloading}
            <div style="align-self: center">
                <Loader/>
            </div>
        {:else if failedMessage}
            <Callout status="failed">
                {failedMessage}
            </Callout>
        {:else}
            <JournalCard {journal}/>
            {#if journal.error}
                <div in:fade|local>
                    <br/>
                    <Callout status="failed" label="error" title="Operation failed">
                        {journal.error}
                    </Callout>
                </div>
            {/if}

            <hr/>
            {#if journal.records.length > 0}
                <p class="records-header">Records</p>
                <br/>
                {#each journal.records as record}
                    <div in:fade>
                        <RecordCard {record}/>
                        <br/>
                    </div>
                {/each}
            {:else}
                <p class="records-header">No records</p>
            {/if}
        {/if}
    </div>
</div>
