<!-- routify:options title="Services" -->
<script lang="ts">
    import {InternalAPI} from "../api";
    import {onDestroy, onMount} from "svelte";
    import Callout from "../_components/Callout.svelte";
    import Loader from "../_components/Loader.svelte";
    import ServiceCard from "../_components/ServiceCard.svelte";
    import {servicesUpdates, Updates} from "../api/updates";
    import {Info} from "../api/internal";

    let updates: Updates<Info>;
    let services: Array<Info> = [];
    let downloading = false;
    let failedMessage = null;

    async function download() {
        downloading = true;
        failedMessage = null;
        try {
            services = await InternalAPI.listServices();
        } catch (e) {
            failedMessage = e.toString();
        } finally {
            downloading = false;
        }
    }

    function serviceUpdated(info: Info) {
        services = services.map((srv) => {
            if (srv.name === info.name) {
                return info;
            }
            return srv;
        })
    }

    async function init() {
        updates = servicesUpdates(serviceUpdated);
        await download()
    }

    onMount(init);
    onDestroy(() => updates.close())
</script>
{#if downloading}
    <div style="align-self: center">
        <Loader/>
    </div>
{/if}

{#if failedMessage}
    <Callout title="failed to download" status="failed" message={failedMessage}/>
    <br/>
{/if}

{#each services as service}
    <ServiceCard {service}/>
    <br/>
{/each}