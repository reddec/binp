<script>
    import Card from "./card/Card.svelte";
    import Content from "./card/Content.svelte";

    export let status = 'pending'
    export let title = ''
    export let message = ''
    export let label = '';
</script>
<Card>
    <Content {status} {title}>
        <slot>{message}</slot>
        <span slot="status">{label || status}</span>
    </Content>
</Card>