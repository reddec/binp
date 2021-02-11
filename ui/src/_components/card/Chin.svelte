<script>
    import {slide} from 'svelte/transition';

    export let status = '';
</script>
<style type="text/scss">
  @import "../../../assets/main";

  .chin {
    text-align: center;
    padding-top: 1em + $padding;
    padding-bottom: $padding;
    border-radius: 0 0 $radius $radius;
    z-index: 0;
    margin-top: -1em;
    font-size: smaller;
  }
</style>
<div class="chin {status}" in:slide|local on:click>
    <slot>
        {status}
    </slot>
</div>