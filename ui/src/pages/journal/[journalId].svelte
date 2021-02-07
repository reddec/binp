<script>
    import {metatags} from '@roxi/routify'
    import JournalCard from "../../_components/JournalCard.svelte";
    import {InternalAPI} from "../../api";
    import {onMount} from "svelte";
    import Loader from "../../_components/Loader.svelte";
    import RecordCard from "../../_components/RecordCard.svelte";
    import Callout from "../../_components/Callout.svelte";
    import {url} from '@roxi/routify'
    import Header from "../../_components/Header.svelte";

    metatags.title = 'BIP'
    metatags.description = 'Basic Integration Platform'

    export let journalId;

    let journal;

    let failedMessage;
    let downloading = true;

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

    onMount(download);

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
<Header title="Journal" backURL="/">
    <a slot="right-action" on:click={download}>
        🗘
    </a>
</Header>
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
                <br/>
                <Callout status="failed">
                    {journal.error}
                </Callout>
            {/if}

            <hr/>
            {#if journal.records.length > 0}
                <p class="records-header">Records</p>
                <br/>
                {#each journal.records as record}
                    <RecordCard {record}/>
                    <br/>
                {/each}
            {:else}
                <p class="records-header">No records</p>
            {/if}
        {/if}
    </div>
</div>
