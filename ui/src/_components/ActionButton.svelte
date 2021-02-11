<script>
    import {InternalAPI} from "../api";
    import Content from "./card/Content.svelte";
    import Card from "./card/Card.svelte";
    import Chin from "./card/Chin.svelte";

    export let action;
    let status = ''
    let failedMessage = '';
    let result = {};

    async function invoke() {
        failedMessage = ''
        status = 'pending'
        try {
            result = await InternalAPI.invokeAction({
                name: action.name
            })
            status = 'success'
        } catch (e) {
            failedMessage = e.toString()
            status = 'failed'
        }
    }


</script>
<Card>
    <Content title={action.name} {status} on:click={invoke}>
        {action.description}
    </Content>
    {#if status && status !== 'pending'}
        <Chin status="{status}">
            {#if status === 'success'}
                {result.duration.toFixed(2)}s
            {:else if status === 'failed'}
                operation failed
            {/if}
        </Chin>
    {/if}
</Card>