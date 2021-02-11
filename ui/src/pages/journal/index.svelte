<!-- routify:options title="Journals" -->
<script lang="ts">
    import {metatags} from '@roxi/routify'
    import JournalCard from "../../_components/JournalCard.svelte";
    import {InternalAPI} from "../../api";
    import {onDestroy, onMount} from "svelte";
    import Loader from "../../_components/Loader.svelte";
    import Callout from "../../_components/Callout.svelte";
    import {journalsHeadlines} from "../../api/updates.ts";

    metatags.title = 'BINP'
    metatags.description = 'Basic Integration Platform'

    const perPage = 20
    export let page = 0;

    let journals = [];

    let downloading = false;
    let hasMore = true;
    let success = false;
    let failedMessage = null;
    let updates;

    async function download(reset = false) {
        if (!hasMore) {
            return;
        }
        success = false;
        downloading = true;
        failedMessage = null;
        if (reset) {
            page = 0;
            journals = [];
        }
        try {
            const batch = await InternalAPI.listJournals({page: page});
            hasMore = batch.length >= perPage;
            journals = journals.concat(batch);
            page += 1;
            success = true;
        } catch (e) {
            failedMessage = e.toString();
        } finally {
            downloading = false;
        }
    }

    function init() {
        updates = journalsHeadlines(update);
        download();
    }

    function update(headline) {
        let updated = false;
        journals = journals.map((j) => {
            if (j.id === headline.id) {
                updated = true;
                return headline
            }
            return j
        })
        if (!updated) {
            journals.unshift(headline);
        }
    }


    onMount(init);
    onDestroy(() => updates.close())

</script>
<style>
    button {
        display: block;
        width: 100%;
        border: none;
        border-top: #333333 dashed 0.1em;
        border-bottom: #333333 dashed 0.1em;
        color: #333333;
        margin: 1em;
        padding: 0.5em;
        font-size: large;
        background-color: white;
        align-self: center;
    }
</style>

{#each journals as journal}
    <JournalCard {journal}/>
    <br/>
{/each}
{#if failedMessage}
    <Callout status="failed">{failedMessage}</Callout>
{/if}
{#if downloading}
    <div style="align-self: center">
        <Loader/>
    </div>
{:else if hasMore}
    <button style="text-align: center" on:click={() => download()}>
        {#if success}
            load more
        {:else}
            reload
        {/if}
    </button>
{/if}
