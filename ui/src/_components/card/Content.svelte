<script>
    import {createEventDispatcher} from "svelte";

    const dispatch = createEventDispatcher();
    export let status = ''
    export let title = ''
    export let tip = '';

</script>
<style type="text/scss">
  @import "../../../assets/main";

  @keyframes showtong {
    0% {
      width: 0;
    }
    100% {
      width: 1em;
    }
  }

  .main {
    display: flex;
    flex-direction: row;

    flex-grow: 1;
    align-items: stretch;
    text-decoration: none;
    color: black;
  }

  .content {
    cursor: pointer;
    flex-grow: 1;
    z-index: 3;
    border-radius: 0 0 $radius 0;
    padding: 0.5em;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .tong {
    text-orientation: sideways;
    writing-mode: vertical-rl;
    text-align: center;
    padding: $padding $padding $padding (1em + $padding);
    border-radius: $radius;
    z-index: 2;
    margin-left: -1em;
    text-transform: uppercase;
    animation: showtong 0.1s ease-in;
  }

  .head {
    display: flex;
    justify-content: space-between;
  }

  .title {
    align-self: center;
    font-size: large;
  }

  .footer {
    display: flex;
    justify-content: space-between;
    font-size: x-small;
  }

  .body {
    padding-top: 1.2em;
    padding-bottom: 1.2em;
    font-size: smaller;
    color: #666666;
  }

  .tip {
    font-size: smaller;
  }


</style>
<div class="main">
    <div class="content">
        {#if $$slots.header || title || tip}
            <div class="head" on:click={()=>dispatch('header-click')}>
                <slot name="header">
                    <span class="title"><slot name="title">{title}</slot></span>
                    <span class="tip muted"><slot name="tip">{tip}</slot></span>
                </slot>
            </div>
        {/if}
        <div class="body" on:click>
            <slot/>
        </div>
        <slot name="append"/>
        <div class="footer muted">
            <slot name="footer"/>
        </div>
    </div>
    {#if status || $$slots.status}
        <div class="tong {status}">
            <slot name="status">{status}</slot>
        </div>
    {/if}
</div>
