<script>
    import {metatags} from '@roxi/routify'
    import JournalCard from "../_components/JournalCard.svelte";
    import {InternalAPI} from "../api";
    import {onMount} from "svelte";
    import Loader from "../_components/Loader.svelte";
    import Header from "../_components/Header.svelte";
    import TopMenu from "../_components/TopMenu.svelte";
    import Callout from "../_components/Callout.svelte";
    import AppBar from "../_components/AppBar.svelte";

    metatags.title = 'BIP'
    metatags.description = 'Basic Integration Platform'

    const perPage = 20
    export let page = 0;

    let journals = [];

    let downloading = false;
    let hasMore = true;
    let success = false;
    let failedMessage = null;

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
<AppBar>
    <Header>
        <span slot="left-action">&nbsp;</span>
        <a slot="right-action" on:click={() => download(true)}>
            🗘
        </a>
        <span>Activities</span>
    </Header>
    <TopMenu/>
</AppBar>


<div class="content">
    <div class="list">
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
    </div>
</div>
