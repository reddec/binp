<script>
    import {isActive, layout, page, url, metatags} from '@roxi/routify'

    let collapse = true;
</script>
<style type="text/scss">
  @import "assets/main";

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
    padding: 0.4em;
  }

  .app-bar {
    position: sticky;
    top: 0;
    z-index: 9999;
  }

  .bar-title {
    z-index: 1000;
    background-color: #1d1d1d;
    color: white;
    padding: 0.1em 0.5em 0.1em 0.5em;
    margin: 0;
    font-size: xx-large;
    text-align: center;
    box-shadow: #1d1d1d 0 0.05em 0.1em;
  }

  .menu {
    display: flex;
    width: 100%;
    justify-content: space-between;
  }

  .menu a {
    margin: 0.4em;
    text-decoration: none;
    color: white;
    padding: 2*$padding;
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
    border-radius: $radius;
  }
</style>
<!-- routify:options preload="proximity" -->

<div class="app-bar">
    <h1 class="bar-title">{$page.title}</h1>
</div>

<div class="secondary">
    <div class="menu">
        {#each $layout.children as {path, title}}
            <a class:active={$isActive(path)} use:$url={{}} href={path}>{title}</a>
        {/each}
    </div>
</div>

<div class="content">
    <div class="list">
        <slot/>
    </div>
</div>