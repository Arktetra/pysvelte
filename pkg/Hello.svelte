<script lang="ts">
    export let name;
</script>

<svelte:options customElement="hello-element" />
<div>
    <h1>Hello, {name}!</h1>
</div>