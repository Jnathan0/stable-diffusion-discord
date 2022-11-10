import discord


class ImageSelect(discord.ui.Select):
    def __init__(self, collage: discord.File, images: list):
        options = [discord.SelectOption(label='Image collage')] + [discord.SelectOption(label=f'Image {i + 1}') for i in range(len(images))]
        super().__init__(placeholder='Select an image',
                         min_values=1, max_values=1, options=options)
        self.collage = collage
        self.images = images

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.values[0] == 'Image collage':
            self.collage.fp.seek(0)
            await interaction.edit_original_message(attachments=[self.collage])
        else:
            image_index = int(self.values[0].split(' ')[-1]) - 1
            self.images[image_index].fp.seek(0)
            await interaction.edit_original_message(attachments=[self.images[image_index]])

class ImageSelectView(discord.ui.View):
    def __init__(self, collage: discord.File, images: list, timeout: float):
        super().__init__(timeout=timeout)
        self.add_item(ImageSelect(collage, images))