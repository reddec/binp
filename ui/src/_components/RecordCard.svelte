<script>
    import dayjs from 'dayjs';
    import JSONTree from 'svelte-json-tree'
    import {slide} from 'svelte/transition';
    import Card from "./card/Card.svelte";
    import Content from "./card/Content.svelte";

    export let record;

    let showFields = false;

    $:fieldsNum = Object.keys(record.params).length
    $:createdAt = dayjs(record.createdAt)
</script>
<style>


    .field {
        margin-bottom: 0.8em;
    }

    .field-name {
        font-weight: bold;
        margin-bottom: 0.2em;
    }


</style>
<Card>
    <Content on:click={()=>showFields = !showFields} title={record.message}>
        {#if showFields}
            <div class="fields" transition:slide|local>
                {#each Object.entries(record.params) as [key, value]}
                    <div class="field">
                        <div class="field-name">{key}</div>
                        <div class="field-value">
                            <JSONTree {value}/>
                        </div>
                    </div>
                {/each}
            </div>
        {:else if fieldsNum > 0 }
            click to see
            {#if fieldsNum > 1}
                {fieldsNum} fields
            {:else}
                {fieldsNum} field
            {/if}

        {/if}
        <span slot="footer">{createdAt.format('DD MMMM YYYY')}</span>
        <span slot="footer">{createdAt.format('HH:mm:ss')}</span>
    </Content>
</Card>
