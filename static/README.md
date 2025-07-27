# Static Files for Element Words

This directory contains static assets for the Element Words application.

## Current Files

### SVG Files (Ready to use)
- `favicon.svg` - SVG favicon with atom emoji
- `og-image.svg` - Open Graph image for social media sharing (1200x630)

### PNG Files (Need to be created)
- `favicon-16x16.png` - 16x16 PNG favicon (placeholder)
- `favicon-32x32.png` - 32x32 PNG favicon (placeholder)
- `og-image.png` - 1200x630 PNG version for social media (placeholder)

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
convert og-image.svg -resize 1200x630 og-image.png

# Using Inkscape
inkscape favicon.svg --export-png=favicon-16x16.png --export-width=16 --export-height=16
inkscape favicon.svg --export-png=favicon-32x32.png --export-width=32 --export-height=32
inkscape og-image.svg --export-png=og-image.png --export-width=1200 --export-height=630
```

## Important Notes

1. **Update Domain URLs**: In `main.py`, replace `https://your-domain.com` with your actual domain name in the Open Graph meta tags.

2. **Social Media Compatibility**: PNG files are more widely supported by social media platforms than SVG files.

3. **File Sizes**: Keep PNG files optimized for web use to ensure fast loading times.

4. **Testing**: Test social media sharing after creating the PNG files using tools like:
   - [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
   - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
   - [Open Graph Preview](https://www.opengraph.xyz/)