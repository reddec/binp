<script>
    import {InternalAPI} from "../api";
    import { slide } from 'svelte/transition';

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
            failedMessage = e.toLocaleString()
            status = 'failed'
        }
    }


</script>
<style>
    @keyframes loading {
        0% {
            color: white;
            background-color: #085b8e;
        }
        50% {
            color: white;
            background-color: #2D9BF0;
        }
        100% {
            color: white;
            background-color: #085b8e;
        }
    }

    .card {
        min-height: 3em;
        display: flex;
        flex-direction: column;
        cursor: pointer;
        flex-grow: 1;
        align-items: stretch;
        text-decoration: none;
        color: black;
    }

    .card-body {
        display: flex;
        flex-grow: 1;
        flex-direction: row;
        align-items: stretch;
    }

    .content {
        flex-grow: 1;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        padding: 0.5em;
        z-index: 3;
        background-color: white;
    }

    .tong {
        text-orientation: sideways;
        writing-mode: vertical-rl;
        text-align: center;
        padding: 0.2em 0.2em 0.2em 1em;
        color: white;
        border-radius: 0.7em;
        border: 0.02em solid black;
        z-index: 2;
        margin-left: -1em;
        text-transform: uppercase;
    }

    .beard {
        text-align: center;
        padding-top: 1.2em;
        padding-bottom: 0.2em;
        color: white;
        border-radius: 0.7em;
        border: 0.02rem solid black;
        z-index: 1;
        margin-top: -1em;
        font-size: smaller;
    }

    .head {
        display: flex;
        justify-content: space-between;
    }

    .title {
        align-self: center;
        font-size: large;
    }

    .body {
        padding-top: 1.2em;
        padding-bottom: 1.2em;
        font-size: smaller;
        color: #666666;
    }

    .success {
        background-color: #79c21b;
        color: white;
    }

    .pending {
        background-color: white;
        color: black;
        animation: loading 2s linear infinite;
    }


    .info {
        color: white;
        background-color: #2D9BF0;
    }

    .failed {
        background-color: #F24726;
        color: white;
    }
</style>
<a class="card" on:click={invoke}>
    <div class="card-body">
        <div class="content">
            <div class="head">
                <span class="title">{action.name}</span>
            </div>
            <div class="body">
                {action.description}
            </div>
        </div>
        {#if status}
            <div class="tong {status}">
                <span>{status}</span>
            </div>
        {/if}
    </div>
    {#if status === 'success'}
        <div class="beard info" in:slide>
            {result.duration.toFixed(2)}s
        </div>
    {:else if status === 'failed'}
        <div class="beard failed" >
            {failedMessage}
        </div>
    {/if}
</a>
