# Static Files for Element Words

This directory contains static assets for the Element Words application.

## Current Files

### SVG Files (Ready to use)
- `favicon.svg` - SVG favicon with atom emoji
- `og-image.svg` - Open Graph image for social media sharing (1200x630)

### PNG Files (Ready to use)
- `favicon-16x16.png` - 16x16 PNG favicon
- `favicon-32x32.png` - 32x32 PNG favicon
- `android-chrome-512x512.png` - 512x512 PNG used for Open Graph sharing (high-res favicon style)

## Converting SVG to PNG

To create the PNG files, you can use:

### Online Tools
- [Convertio](https://convertio.co/svg-png/)
- [CloudConvert](https://cloudconvert.com/svg-to-png)
- [SVG to PNG Converter](https://svgtopng.com/)

### Design Tools
- Figma
- Canva
- GIMP
- Adobe Illustrator

### Command Line (if available)
```bash
# Using ImageMagick
convert favicon.svg -resize 16x16 favicon-16x16.png
convert favicon.svg -resize 32x32 favicon-32x32.png
convert favicon.svg -resize 512x512 android-chrome-512x512.png

# Using Inkscape
inkscape favicon.svg --export-png=favicon-16x16.png --export-width=16 --export-height=16
inkscape favicon.svg --export-png=favicon-32x32.png --export-width=32 --export-height=32
inkscape favicon.svg --export-png=android-chrome-512x512.png --export-width=512 --export-height=512
```

## Important Notes

1. **Update Domain URLs**: In `main.py`, replace `https://your-domain.com` with your actual domain name in the Open Graph meta tags.

2. **Social Media Compatibility**: PNG files are more widely supported by social media platforms than SVG files. We now use a 512x512 favicon-style image for Open Graph sharing instead of the traditional large banner format.

3. **File Sizes**: The 512x512 PNG is optimized for web use (under 5KB) ensuring fast loading times while maintaining high quality for sharing previews.

4. **Testing**: Test social media sharing after creating the PNG files using tools like:
   - [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
   - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
   - [Open Graph Preview](https://www.opengraph.xyz/)