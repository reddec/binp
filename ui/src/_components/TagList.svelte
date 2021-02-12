<script>
    import { createEventDispatcher } from 'svelte';

    export let tags;
    export let status = 'info';

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

  .tag {
    cursor: pointer;
    border-radius: $radius;
    padding: $padding;
    margin: $padding;

  }
</style>
<div class="list">
    {#each tags as tag}
        <span class="tag {status}" on:click={()=> dispatch('click', tag)}>{tag}</span>
    {/each}
</div>