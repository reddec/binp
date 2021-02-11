<!-- routify:options title="Actions" -->
<script>
    import {InternalAPI} from "../api";
    import {onMount} from "svelte";
    import ActionButton from "../_components/ActionButton.svelte";
    import Loader from "../_components/Loader.svelte";
    import Callout from "../_components/Callout.svelte";


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

