<script>
    export let status = 'pending'
    export let zIndex = '0';
    export let action = false;
</script>
<style>
    .block {
        border-radius: 0.7em;
        border: 0.02rem solid black;
        background-color: white;
        padding: 0.5em;
    }
    .success {
        background-color: #79c21b;
        color: white;
    }

    .pending {
        background-color: white;
        color: black;
    }

    .failed {
        background-color: #F24726;
        color: white;
    }

    .info {
        color: white;
        background-color: #2D9BF0;
    }

    .action {
        cursor: pointer;
    }
</style>
<div class="block {status}" style="z-index: {zIndex}" class:action={action}>
    <slot/>
</div>