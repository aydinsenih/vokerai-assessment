<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { onMount } from "svelte";

    interface Order {
        order_number: number;
        burger: number;
        fries: number;
        drink: number;
    }

    let message = $state("");
    let orders: Order[] = $state([]);
    let totalBurgers = $derived(
        orders.reduce((sum, order) => sum + Number(order.burger), 0)
    );
    let totalFries = $derived(
        orders.reduce((sum, order) => sum + Number(order.fries), 0)
    );
    let totalDrinks = $derived(
        orders.reduce((sum, order) => sum + Number(order.drink), 0)
    );

    onMount(() => {
        //get orders
        fetch("http://localhost:8000/orders")
            .then((res) => res.json())
            .then((data) => {
                orders = [];
                orders.push(...data.orders);
            });
    });

    function onRunClick() {
        fetch("http://localhost:8000/order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt: message }),
        })
            .then((res) => res.json())
            .then((data) => {
                orders = [];
                orders.push(...data.orders);
                message = "";
            });
    }
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Counters -->
    <div class="flex flex-row justify-between">
        <div class="p-6 border rounded-lg shadow-sm min-w-48">
            <h2 class="text-lg font-semibold text-center mb-2">
                Total # of burgers
            </h2>
            <p class="text-3xl text-center">{totalBurgers}</p>
        </div>
        <div class="p-6 border rounded-lg shadow-sm min-w-48">
            <h2 class="text-lg font-semibold text-center mb-2">
                Total # of fries
            </h2>
            <p class="text-3xl text-center">{totalFries}</p>
        </div>
        <div class="p-6 border rounded-lg shadow-sm min-w-48">
            <h2 class="text-lg font-semibold text-center mb-2">
                Total # of drinks
            </h2>
            <p class="text-3xl text-center">{totalDrinks}</p>
        </div>
    </div>

    <!-- Message Input -->
    <div class="flex gap-4 py-10">
        <div class="flex-1">
            <div class="relative">
                <input
                    type="text"
                    id="message"
                    bind:value={message}
                    placeholder="Ex: 'I would like one burger and an order of fries', 'Cancel order #2'"
                    class="w-full p-4 border rounded-lg"
                />
            </div>
        </div>
        <div class="flex-2">
            <Button
                style="border-radius: 50%;"
                variant="default"
                class="self-end size-14"
                on:click={() => onRunClick()}>run</Button
            >
        </div>
    </div>

    <!-- Order History -->
    <div>
        <h2 class="text-xl font-semibold mb-4">Order History</h2>
        <div class="space-y-3">
            {#each orders as order}
                <div
                    class="p-4 border rounded-lg flex justify-between items-center"
                >
                    <span class="font-medium">Order #{order.order_number}</span>
                    <span>
                        {[
                            order.burger > 0
                                ? `${order.burger} burger(s)`
                                : undefined,
                            order.fries > 0
                                ? `${order.fries} fries`
                                : undefined,
                            order.drink > 0
                                ? `${order.drink} drink(s)`
                                : undefined,
                        ]
                            .filter((item) => item !== undefined)
                            .join(", ")}</span
                    >
                </div>
            {/each}
        </div>
    </div>
</div>
