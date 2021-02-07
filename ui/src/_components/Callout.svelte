<script>
    import Card from "./Card.svelte";

    export let status = 'pending'
</script>
<Card  status="{status}">
    <slot/>
</Card>