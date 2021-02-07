<script>
    import dayjs from 'dayjs';
    import JSONTree from 'svelte-json-tree'
    import { slide, fade } from 'svelte/transition';
    export let record;

    let showFields = false;

    $:fieldsNum = Object.keys(record.params).length
    $:createdAt = dayjs(record.createdAt)
</script>
<style>
    .card {
        display: flex;
        flex-direction: column;

        align-items: stretch;
        text-decoration: none;
        color: black;
    }

    .info {
        cursor: pointer;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        padding: 0.5em;
        background-color: white;
        z-index: 3;
    }

    .fields {
        padding: 2.2em 0.5em 0.2em;
        border-radius: 0.7em;
        border: 0.13em solid black;
        z-index: 2;
        margin-top: -2em;
        background-color: white;
        font-size: smaller;
    }

    .tong {
        text-align: center;
        padding-top: 1.2em;
        padding-bottom: 0.2em;
        color: white;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        z-index: 1;
        margin-top: -1em;
        background-color: #2D9BF0;
        font-size: smaller;
    }


    .field {
        margin-bottom: 0.8em;
    }

    .field-name {
        font-weight: bold;
        margin-bottom: 0.2em;
    }

    .footer {
        display: flex;
        justify-content: space-between;
        font-size: x-small;
    }

    .body {
        padding-top: 0.2em;
        padding-bottom: 0.4em;
        color: #666666;
    }

    .muted {
        align-self: center;
        color: #999999;
    }

</style>

<div class="card">
    <div class="info" on:click={()=>showFields = !showFields}>
        <div class="body">{record.message}</div>
        <div class="footer">
            <span class="muted">{createdAt.format('DD MMMM YYYY')}</span>
            <span class="muted">{createdAt.format('HH:mm:ss')}</span>
        </div>
    </div>
    {#if fieldsNum > 0}
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
        {/if}
            <div class="tong" on:click={()=>showFields = !showFields}>
            <span>
                {#if fieldsNum > 1}
                    {fieldsNum} fields
                {:else}
                    {fieldsNum} field
                {/if}
            </span>
            </div>


    {/if}
</div>