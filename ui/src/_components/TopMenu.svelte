<script>
    import {isActive, url} from '@roxi/routify'
</script>
<style type="text/scss">
  @import "assets/main";

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

<div class="secondary">
    <div class="menu">
        <a href="/" use:$url={{}} class:active={$isActive('/index')}>Activities</a>
        <a href="/services" use:$url={{}} class:active={$isActive('/services')}>Services</a>
        <a href="/actions" use:$url={{}} class:active={$isActive('/actions')}>Actions</a>
    </div>
</div>
