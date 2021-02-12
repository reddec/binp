<!-- routify:options title="Journals" -->
<script lang="ts">
    import {metatags} from '@roxi/routify'
    import JournalCard from "../../_components/JournalCard.svelte";
    import {InternalAPI} from "../../api";
    import {onDestroy, onMount} from "svelte";
    import Loader from "../../_components/Loader.svelte";
    import Callout from "../../_components/Callout.svelte";
    import {journalsHeadlines} from "../../api/updates.ts";
    import {Query} from "../../api/internal";
    import TagList from "../../_components/TagList.svelte";
    import OneOf from "../../_components/OneOf.svelte";

    metatags.title = 'BINP'
    metatags.description = 'Basic Integration Platform'

    const perPage = 20
    const completionOptions = {
        '': 'all',
        'finished': 'finished',
        'pending': 'pending',
        'failed': 'failed',
        'success': 'success',
    }
    let completionStatus = '';

    export let page = 0;

    let journals = [];


    let downloading = false;
    let hasMore = true;
    let success = false;
    let failedMessage = null;
    let updates;

    let conditions: Query = {};

    function normalizeConditions() {
        if (!conditions.operation) {
            conditions.operation = undefined
        }
        if (conditions.labels && conditions.labels.length === 0) {
            conditions.labels = undefined;
        }
        conditions.pending = undefined;
        conditions.failed = undefined;
        if (completionStatus === 'finished') {
            conditions.pending = false;
        } else if (completionStatus === 'pending') {
            conditions.pending = true;
        } else if (completionStatus === 'failed') {
            conditions.failed = true;
        } else if (completionStatus === 'success') {
            conditions.failed = false;
            conditions.pending = false;
        }
    }

    async function download(reset = false) {
        if (!hasMore && !reset) {
            return;
        }
        normalizeConditions();
        success = false;
        downloading = true;
        failedMessage = null;
        if (reset) {
            page = 0;
            journals = [];
        }
        try {
            const batch = await InternalAPI.searchJournals({page: page, query: conditions});
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
        if (!updated && !hasQuery) {
            journals.unshift(headline);
        }
    }

    async function addQueryTag({detail}) {
        if (!conditions.labels) {
            conditions.labels = []
        } else if (conditions.labels.indexOf(detail) !== -1) {
            return
        }
        conditions.labels = conditions.labels.concat([detail])
        await download(true)
    }

    async function removeQueryTag({detail}) {
        if (!conditions.labels) {
            return
        }
        conditions.labels = conditions.labels.filter((x) => x !== detail)
        await download(true)
    }

    async function addQueryOperation(operation) {
        if (conditions.operation === operation) {
            return
        }
        conditions.operation = operation
        await download(true)
    }

    async function removeQueryOperation() {
        if (!conditions.operation) {
            return
        }
        conditions.operation = undefined
        await download(true)
    }

    async function setQueryStatus({detail}) {
        if (completionStatus === detail) {
            return
        }
        completionStatus = detail;
        await download(true);
    }


    $: hasQuery = JSON.stringify(conditions) !== '{}'

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

    .query {
        margin-bottom: 1em;
    }

    .line {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .line :first-child {
        font-weight: bold;
    }

</style>
<div class="query muted">
    {#if conditions.operation}
        <div class="line">
            <span>Operation:</span>
            <span style="cursor: pointer" on:click={removeQueryOperation}>{conditions.operation}</span>
        </div>
    {/if}
    {#if conditions.labels && conditions.labels.length > 0}
        <div class="line">
            <span>Tags:</span>
            <TagList tags={conditions.labels} on:click={removeQueryTag}/>
        </div>
    {/if}
    <div class="line">
        <span>Status:</span>
        <OneOf selected={completionStatus} options={completionOptions} on:click={setQueryStatus}/>
    </div>
</div>
{#each journals as journal}
    <JournalCard {journal}
                 on:header-click={()=>addQueryOperation(journal.operation)}
                 on:tag-click={addQueryTag}/>
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
