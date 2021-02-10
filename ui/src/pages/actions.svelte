<script>
    import Header from "../_components/Header.svelte";
    import TopMenu from "../_components/TopMenu.svelte";
    import {InternalAPI} from "../api";
    import {onMount} from "svelte";
    import ActionButton from "../_components/ActionButton.svelte";
    import Loader from "../_components/Loader.svelte";
    import Callout from "../_components/Callout.svelte";
    import AppBar from "../_components/AppBar.svelte";


    let actions = [];
    let downloading = false;
    let failedMessage = null;

    async function download() {
        downloading = true;
        failedMessage = null;
        try {
            actions = await InternalAPI.listActions();
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
</style>
<AppBar>
    <Header>
        <span slot="left-action">&nbsp;</span>
        <span>Actions</span>
    </Header>
    <TopMenu/>
</AppBar>
<div class="content">
    <div class="list">
        {#if failedMessage}
            <Callout status="failed">
                {failedMessage}
            </Callout>
            <br/>
        {/if}
        {#if downloading}
            <div style="align-self: center">
                <Loader/>
            </div>
        {/if}
        {#each actions as action}
            <ActionButton {action}/>
            <br/>
        {/each}
    </div>
</div>

