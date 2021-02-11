<script lang="ts">
    import {Info} from "../api/internal";
    import Card from "./card/Card.svelte";
    import Content from "./card/Content.svelte";
    import Chin from "./card/Chin.svelte";
    import {InternalAPI} from "../api";
    import {Status} from "../api/internal";

    export let service: Info;

    const statusMapper = {
        'running': 'success',
        'stopped': 'info',
        'restarting': 'pending'
    }
    let errorMessage = '';
    let toggling = false;

    async function toggle() {
        if (toggling) return;
        toggling = true;
        errorMessage = '';
        try {
            await InternalAPI.manageService({
                name: service.name,
                serviceControl: {
                    running: toBeStarted
                }
            })
        } catch (e) {
            errorMessage = e.toString()
        } finally {
            toggling = false;
        }
    }

    $:toBeStarted = (service.status === 'stopped');
    $:status = statusMapper[service.status];
    $:tip = service.autostart ? 'autostart' : 'manual';
    $:restart = service.restart ? 'auto-restart' : 'no restart';

</script>


<Card>
    <Content title="{service.name}" {status} {tip} on:click={toggle}>
        {service.description}
        <span slot="status">
        {service.status === Status.Restarting ? 'restart...' : service.status}</span>
        <span slot="footer">{restart}</span>
        <span slot="footer">
            {#if service.restart}
            restart delay {service.restartDelay}s
            {/if}
        </span>
    </Content>
    {#if errorMessage}
        <Chin status="error">{errorMessage}</Chin>
    {:else if toggling}
        <Chin status="pending">toggling...</Chin>
    {:else}
        <Chin status="info">click to
            {#if toBeStarted}start{:else}stop{/if}
        </Chin>
    {/if}

</Card>