<script>
    import {createEventDispatcher} from "svelte";

    export let options = {}
    export let selected;

    const dispatch = createEventDispatcher();
</script>

<style lang="scss">
  @import "assets/main";

  .list {
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    font-size: small;
  }

  .option {
    cursor: pointer;
    border-radius: $radius;
    padding: $padding;
    margin: $padding;
  }

  .outlined {
    border: 0.02rem solid black;
  }
</style>
<div class="list">
    {#each Object.entries(options) as [value, title]}
        <span class="option" class:info={value === selected} class:outlined={value !== selected}
              on:click={()=> dispatch('click', value)}>{title}</span>
    {/each}
</div>