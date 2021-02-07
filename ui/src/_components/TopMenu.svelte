<script>
    import {isActive, url} from '@roxi/routify'
</script>
<style>
    .menu {
        display: flex;
        width: 100%;
        justify-content: space-between;
    }

    .menu a {
        margin: 0.4em;
        text-decoration: none;
        color: white;
        padding: 0.4em;
    }

    .secondary {
        display: flex;
        background-color: #666666;
        color: white;
        box-shadow: #666666 0 0.05em 0.2em;
        justify-content: space-between;
    }

    .active {
        background-color: #999999;
        border-radius: 0.7em;
    }

</style>

<div class="secondary">
    <div class="menu">
        <a href="/" use:$url={{}} class:active={$isActive('/index')}>📰 Activities</a>
        <a href="/actions" use:$url={{}} class:active={$isActive('/actions')}>🔲 Actions</a>
    </div>
</div>
