<script>
    import {url} from '@roxi/routify'

    export let backURL = '../'
    export let title = 'HEADER'
</script>
<style>
    .header {

        display: flex;
        flex-direction: column;
        z-index: 100;
    }

    .main {
        display: flex;
        z-index: 10;
        background-color: #1d1d1d;
        color: white;
        padding: 0.1em 0.5em 0.1em 0.5em;
        margin: 0;
        font-size: xx-large;
        align-items: baseline;
        justify-content: space-between;
        box-shadow: #1d1d1d 0 0.05em 0.1em;
    }


    .header * {
        text-decoration: none;
        color: white;
    }

    .title {
        justify-self: center;
    }
</style>

<div class="header">
    <div class="main">
        <slot name="left-action">
            <a href="{backURL}" use:$url={{}}>
                🡄
            </a>
        </slot>
        <span class="title">
        <slot>
            {title}
        </slot>
        </span>
        <slot name="right-action">
            &nbsp;
        </slot>
    </div>
</div>